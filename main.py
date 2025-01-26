from fastapi import FastAPI as runnable_servers


app = runnable_servers()

@app.get('/')
def testing_servers():
    return {"message": "We, are ready to go"}
@app.get('/admin')
def testing_servers():
    return {"message": "We, are ready to go admin"}