
from app import create_app

app = create_app()
app.run(debug=True)


#favor tener instalado sqlalchemy 
#pip install sqlalchemy==1.4.29