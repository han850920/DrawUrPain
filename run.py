from app import app
if __name__ == '__main__':
    # app.config['TEMPLATES_AUTO_RELOAD'] = True  
    # app.config['FLASK_DEBUG'] = 1    
    # app.jinja_env.auto_reload = True
    app.run(host='140.114.79.84', port=8888, debug=True)
