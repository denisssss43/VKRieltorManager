if __name__ == "__main__":
    import os
    
    os.system('set FLASK_APP=web-server/main.py')
    os.system('cd web-server & flask run')