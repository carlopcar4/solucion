import './Login.css';
import { useNavigate, Link } from 'react-router-dom';



function Login() {
    const navegar = useNavigate();

    function handleSubmit(e) {
        e.preventDefault();
        const { username, password } = e.target

        fetch('http://localhost:4000/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                username: username.value.trim(),
                password: password.value
            })
        })
            .then(r => (r.ok ? navegar('/') : alert('Credenciales incorrectas')))
            .catch(() => alert('Error de conexión'));
    }

    return(
        <div className='aut'>
            <h1>Log in</h1>
            <p>To use this service, you must be a user of "Portal Provincial de la diputación de Sevilla</p>

            <form onSubmit={handleSubmit} className='form-box'>
                
                {/* <p>New? <Link to={'/CreateAccount'}>Create an account</Link></p> */}
                <hr />

                <label>Usuario*
                    <input type="text" name="username" required/>
                </label>

                <label>Contraseña*
                    <input type="password" name='contraseña' required/>
                </label>
                <hr />

                <button type='submit' className='boton-si'>Log in</button>
            </form>
        </div>
    )
}

export default Login;