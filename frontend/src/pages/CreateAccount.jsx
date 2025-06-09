import './Login.css';
import { useNavigate, Link } from 'react-router-dom';


function CreateAccount() {

    function handleSubmit(e) {
        e.preventDefault();

        const username = e.target.username.value;
        const password = e.target.password.value;

        fetch("http://localhost:4000/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ username, password }),
        })
            .then((res) => {
                if (res.ok) {
                    navigate('/');
                } else {
                    alert("Credenciales incorrectas");
                }
            })
            .catch((error) => {
                console.error("Error al crear la cuenta:", error);
                alert("Error de conexión con el servidor");
            });
    }

    return (
        <div className='login-container'>
            <h1>Create Account</h1>

            <form onSubmit={handleSubmit} className='form-box'>
                <p>Already have an account? <Link to="/login">Log in</Link></p>
                <hr />
                <label className='form-label'>Username*
                    <input type="text" name='username' required />
                </label>
                <label className='form-label'>Password*
                    <input type="password" name='password' required />
                </label>
                <hr />
                <button type='submit' className='boton-si'>Create</button>
            </form>
        </div>
    )
}



export default CreateAccount;
