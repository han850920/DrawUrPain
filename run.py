from app import app
if __name__ == '__main__':
    # app.config['TEMPLATES_AUTO_RELOAD'] = True  
    # app.config['FLASK_DEBUG'] = 1    
    # app.jinja_env.auto_reload = True
    app.run(host='0.0.0.0', port=8988, debug=True)
