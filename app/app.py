import os
from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from schema import PostGet, Response
from datetime import datetime
import sqlalchemy
from sqlalchemy import create_engine, select
from catboost import CatBoostClassifier
import pandas as pd
import uvicorn
from loguru import logger
import json
import yaml
import hashlib
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")
app = FastAPI()

logger.info('Reading DB credentials')
if not os.path.exists(os.path.join(os.getcwd(), 'db_creds.yaml')):
    raise RuntimeError('db_creds.yaml not found. Unable to start')
with open('db_creds.yaml', encoding="utf-8") as f:
    db_creds = yaml.safe_load(f)

db_url = sqlalchemy.engine.URL.create(**db_creds)

logger.info('Creating engine')
engine = create_engine(db_url)

metadata_obj = sqlalchemy.MetaData()
metadata_obj.reflect(bind=engine, only=['user_data', 'post_text_df', 'feed_data'])

logger.info('Query df_post')
df_post = pd.read_sql(select(metadata_obj.tables['post_text_df']), engine)
df_post.post_id = df_post.post_id.astype(int)

logger.info('Query df_user')
df_user = pd.read_sql(select(metadata_obj.tables['user_data']), engine)
df_user.user_id = df_user.user_id.astype(int)

logger.info('Query liked post')
liked_df = pd.read_sql('''
 SELECT user_id, array_agg(post_id)
 FROM public.feed_data
 WHERE target = 1
 GROUP BY user_id
 ORDER BY user_id
 ''', engine).set_index('user_id')

logger.info('Loading model')
model = CatBoostClassifier()
model.load_model('catboost_model.cbm')


def get_exp_group(user_id: int, test_size=0.5, salt='some_default_salt') -> str:
    """Returns 'test' or 'control', based on the ID and salt"""
    hex_hash_str = hashlib.md5((salt + str(user_id)).encode()).hexdigest()
    bucket = int(hex_hash_str, 16) % 100
    if bucket < test_size * 100:
        return 'test'
    else:
        return 'control'


@app.get("/post/recommendations/", response_model=List[PostGet], summary="recommendations")
def recommended_posts(
        id: int,
        time: datetime,
        limit: int = 10) -> List[PostGet]:
    """Returns recommendations"""
    if id not in df_user.user_id.values:
        raise HTTPException(status_code=400, detail="User doesn't exist")
    df = df_post.assign(**df_user.loc[df_user.user_id == id].squeeze().to_dict())
    df['hour'] = time.hour
    df['dayofweek'] = time.weekday()
    df['day'] = time.day
    df['preds'] = model.predict_proba(df[['hour', 'dayofweek', 'day', 'gender', 'age', 'country', 'city',
                                          'exp_group', 'os', 'source', 'text', 'topic']])[:, 1]
    df = df[~df.post_id.isin(liked_df.loc[id].squeeze())]
    return list(df.rename(columns={'post_id': 'id'})
                .sort_values('preds', ascending=False)[:limit]
                .to_records(index=False))


@app.get("/post/recommendations/ab/", response_model=Response, summary="recommendations AB test")
def recommended_posts_ab(
        id: int,
        time: datetime,
        limit: int = 10) -> Response:
    """
    Returns 'test' or 'control 'experiment group, for AB testing, and recommendations.
    Control group recommendations are random. Test group recommendations are predicted by model.
    """
    if id not in df_user.user_id.values:
        raise HTTPException(status_code=400, detail="User doesn't exist")
    exp_group = get_exp_group(user_id=id)
    if exp_group == 'control':
        return {'exp_group': exp_group, 'recommendations': list(df_post.rename(columns={'post_id': 'id'})
                                                                .sample(limit)
                                                                .to_records(index=False))}
    elif exp_group == 'test':
        return {'exp_group': exp_group, 'recommendations': recommended_posts(id, time, limit)}
    else:
        raise ValueError('unknown group')


@app.get("/userlist", summary='get all users id')
def userlist():
    """Returns users quantity and IDs"""
    ul = df_user.user_id.unique().tolist()
    return {'count': len(ul), 'ids': ul}


@app.get("/healthcheck", summary='healthcheck')
def healthcheck():
    """Healthcheck endpoint"""
    if ((isinstance(df_post, pd.DataFrame) and not df_post.empty) and
            (isinstance(df_user, pd.DataFrame) and not df_user.empty) and
            (isinstance(liked_df, pd.DataFrame) and not liked_df.empty) and
            (isinstance(model, CatBoostClassifier) and model.is_fitted())):
        return {'status': 'ok'}
    logger.error('Some dataframe or model error on healthcheck!')
    raise HTTPException(status_code=500, detail='Something gone wrong')


@app.get("/download/{file_name}", summary="download 'user_data', 'post_text_df', 'feed_data'")
async def get_user_data(file_name: str):
    """Download endpoint for 'user_data', 'post_text_df', 'feed_data'"""
    if file_name not in ['user_data', 'post_text_df', 'feed_data']:
        return {"status": "only 'user_data', 'post_text_df' or 'feed_data' allowed for download"}
    path = Path.cwd().parent/'bd'/f'{file_name}.csv'
    if path.is_file():
        headers = {"Content-Disposition": "attachment; filename=user_data.csv"}
        return FileResponse(path, media_type="application/csv", headers=headers)
    else:
        return {"status": "file doesn't exist"}


if __name__ == "__main__":
    logger.info('Run uvicorn')
    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info")
