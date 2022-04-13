#!/usr/bin/env python
# coding: utf-8

# ### Library

# In[7]:


import os
import pymysql
import pandas as pd
import pickle

from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash


# ### Table Name

# In[21]:


MYSQL_TABLE_RISK_DATA = 'risk_data'
MYSQL_TABLE_API_USER = 'api_user'
MYSQL_TABLE_RISK_CRITERIA = 'risk_criteria'


# ### SQL Connection Setting

# In[3]:


def connectSQL():
    load_dotenv()
    MYSQL_USER = os.getenv('MYSQL_USER')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
    MYSQL_PORT = os.getenv("MYSQL_PORT")
    MYSQL_HOST = os.getenv("MYSQL_HOST")
    MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")
    conn = pymysql.connect(host = MYSQL_HOST, port = int(MYSQL_PORT), user = MYSQL_USER, passwd = MYSQL_PASSWORD, db = MYSQL_DATABASE)
    return conn


# ### API User ( For Auth of using API )
# ---
# #### Table Structure
# 

# In[24]:


def createAPIUser(username, password):
    sql_command = 'INSERT INTO ' + MYSQL_TABLE_API_USER + ' VALUES (\''
    hash_password = generate_password_hash(password)
    sql_command = sql_command + username + '\',\'None\' ,\'' + hash_password + '\');'
    conn = connectSQL()
    
    try:
        with conn.cursor() as cur:
            cur.execute(sql_command)
            conn.commit()
    finally:
        conn.close()
        
def deleteAPIUser(username):
    sql_command = 'DELETE FROM ' + MYSQL_TABLE_API_USER + ' WHERE account = \'' + username + '\''
    conn = connectSQL()
    
    try:
        with conn.cursor() as cur:
            cur.execute(sql_command)
            conn.commit()
    finally:
        conn.close()


# In[9]:


def checkValidation(username, password):
    sql_command = 'SELECT password_hash FROM ' + MYSQL_TABLE_API_USER + ' WHERE account = \'' + username + '\''
    conn = connectSQL()
    
    try:
        with conn.cursor() as cur:
            cur.execute(sql_command)
            return check_password_hash(cur.fetchone()[0], password)
    finally:
        conn.close()


# ### Risk Evaluation User
# ---
# #### Table Structure

# In[10]:


def getAllUser():
    sql_command = "SELECT * FROM risk_data"
    conn = connectSQL()
    
    try:
        with conn.cursor() as cur:
            cur.execute(sql_command)
            return cur.fetchall()
    finally:
        conn.close()


# In[11]:


def getAllUserInLog():
     with open('user_list', 'rb') as f:
        return pickle.load(f)


# In[12]:


def getAllNewUser():
    allUser = getAllUser()
    logUser = getAllUserInLog()
    newUser = []
    
    for user in logUser:
        if user not in [item[0] for item in allUser] and user != '-':
            newUser.append(user)
    return newUser


# In[25]:


def createUser(username, riskscore = 0.5):
    sql_command = 'INSERT INTO ' + MYSQL_TABLE_RISK_DATA + ' VALUES (\''
    sql_command = sql_command + username + '\',\'' + str(riskscore) + '\', NOW());' 
    conn = connectSQL()
    
    try:
        with conn.cursor() as cur:
            cur.execute(sql_command)
            conn.commit()
    finally:
        conn.close()


def deleteUser(username):
    sql_command = 'DELETE FROM ' + MYSQL_TABLE_RISK_DATA + ' WHERE account = \'' + username + '\''
    conn = connectSQL()
    
    try:
        with conn.cursor() as cur:
            cur.execute(sql_command)
            conn.commit()
    finally:
        conn.close()
        
        
# In[14]:


def updateAllNewUser():
    newUser = getAllNewUser()
    for user in newUser:
        createUser(user)


# In[17]:


def updateUser(username, riskscore):
    sql_command = 'UPDATE ' + MYSQL_TABLE_RISK_DATA + ' SET riskScore = \'' + str(riskscore) + '\',lastUpdateTime = NOW()'
    sql_command = sql_command + ' WHERE account = \'' + username + '\';'
    conn = connectSQL()
    
    try:
        with conn.cursor() as cur:
            cur.execute(sql_command)
            conn.commit()
    finally:
        conn.close()


# In[18]:


def getUser(username):
    sql_command = "SELECT * FROM risk_data WHERE account = \'" + username + '\';' 
    conn = connectSQL()
    
    try:
          with conn.cursor() as cur:
            cur.execute(sql_command)
            return cur.fetchone()
    finally:
        conn.close()


# In[19]:


def getRiskScore(username):
    return getUser(username)[1]


# In[20]:



# ### Risk Evaluation Criteria
# ---
# #### Table Structure

# In[22]:


def addRiskCriteria(riskValue, lowerBound):
    sql_command = 'INSERT INTO ' + MYSQL_TABLE_RISK_CRITERIA + ' VALUES (\''
    sql_command = sql_command + riskValue + '\',\'' + lowerBound + '\');'
    conn = connectSQL()
    
    try:
        with conn.cursor() as cur:
            cur.execute(sql_command)
            conn.commit()
    finally:
        conn.close()


# In[23]:


def updateCriteria(oldRiskValue, newRiskValue, lowerBound):
    sql_command = 'UPDATE ' + MYSQL_TABLE_RISK_CRITERIA
    sql_command = sql_command + ' SET lowerBound = \'' + lowerBound + '\', riskValue = \'' + newRiskValue + '\' WHERE riskValue = \'' + oldRiskValue + '\';'
    conn = connectSQL()
    
    try:
        with conn.cursor() as cur:
            cur.execute(sql_command)
            conn.commit()
    finally:
        conn.close()
    
def getAllCriteria():   
    sql_command = "SELECT * FROM " + MYSQL_TABLE_RISK_CRITERIA
    conn = connectSQL()
    
    try:
        with conn.cursor() as cur:
            cur.execute(sql_command)
            return cur.fetchall()
    finally:
        conn.close()
        
def getLowerBound(riskValue):
    sql_command = "SELECT lowerBound FROM "+ MYSQL_TABLE_RISK_CRITERIA +" WHERE riskValue = \'" + riskValue + '\';' 
    conn = connectSQL()
    
    try:
          with conn.cursor() as cur:
            cur.execute(sql_command)
            return cur.fetchone()
    finally:
        conn.close()
        
def getRiskValue(lowerBound):
    sql_command = "SELECT riskValue FROM "+ MYSQL_TABLE_RISK_CRITERIA +" WHERE lowerBound = \'" + lowerBound + '\';' 
    conn = connectSQL()
    
    try:
          with conn.cursor() as cur:
            cur.execute(sql_command)
            return cur.fetchone()
    finally:
        conn.close()
        
def deleteCriteria(riskValue):
    sql_command = 'DELETE FROM ' + MYSQL_TABLE_RISK_CRITERIA + ' WHERE riskValue = \'' + riskValue + '\''
    conn = connectSQL()
    
    try:
        with conn.cursor() as cur:
            cur.execute(sql_command)
            conn.commit()
    finally:
        conn.close()
            


# In[ ]:
####
def getRiskValue(score):
    level = ''
    query = "SELECT * FROM " + MYSQL_TABLE_RISK_CRITERIA
    maxmize = 1
    try:
        conn = connectSQL()
        tempdf = pd.read_sql(query, conn)
        for i in range(len(tempdf['lowerBound'])):
            if tempdf['lowerBound'][i] >= score:
                continue
            else:
                if maxmize > score - tempdf['lowerBound'][i]:
                    maxmize = score - tempdf['lowerBound'][i]
                    level = tempdf['riskValue'][i]
        return level
    except:
        return ({"msg": "SQL Connection Error"}), 401


