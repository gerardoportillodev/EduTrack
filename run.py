
from app import create_app

app = create_app()
app.run(debug=True)


# if __name__ == '__main__':
#favor tener instalado sqlalchemy 
#pip install sqlalchemy==1.4.29