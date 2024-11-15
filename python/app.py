from flask import Flask, redirect, url_for
from auth import auth_blueprint  # Importa el blueprint
from instructor import instructor_blueprint
from clases import clase_blueprint
from turno import turno_blueprint
from estudiante import estudiante_blueprint
from equipamiento import equipamiento_blueprint
from administrativo import administrativo_blueprint


app = Flask(
    __name__,
    template_folder="../html",   
    static_folder="../styles"    
)

app.secret_key = 'tu_secreto'  # Necesario para flash y sesiones

# Registra el blueprint y se asegura de que tenga el prefijo `auth`
app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(instructor_blueprint)
app.register_blueprint(estudiante_blueprint)
app.register_blueprint(clase_blueprint)
app.register_blueprint(turno_blueprint)
app.register_blueprint(equipamiento_blueprint)
app.register_blueprint(administrativo_blueprint)


# Redirige la ruta principal a la página de login del blueprint `auth`
@app.route('/')
def home():
    return redirect(url_for('auth.login'))

if __name__ == "__main__":
    app.run(debug=True)
