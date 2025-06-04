import React, { useState, useRef } from 'react';
import './CreateCouncil.css';
import { useNavigate } from 'react-router-dom';


function CreateCouncil() {
    /* Datos de prueba */
    const provincias = {
        Sevilla: ['Sevilla', 'Dos Hermanas', 'Utrera'],
        Córdoba: ['Adamuz', 'Alcaracejos', 'Almendinilla']
    };

    const colaboraciones = [
        'Proposals', 'Surveys', 'Anonimous proposals',
        'Sortitions', 'Participatory texts', 'Citizen Forum',
        'Policy proposals', 'Budgeting']

    const servicios = [
        'DA Support', 'Meetings', 'KM Support', 'Notification', 'Delegation',
        'IR Capacity', 'Debate', 'Transparency', 'Census', 'Decissions']


    // Estado principal

    const [nombre, setNombre] = useState('');
    const [provincia, SetProvincia] = useState('');
    const [poblacion, SetPoblacion] = useState('');
    const [puerto1, SetPuerto1] = useState(3001);
    const [puerto2, SetPuerto2] = useState(3002);
    const [multi, setMulti] = useState(false);
    const [colSel, SetColSel] = useState([]);
    const [serSel, SetSerSel] = useState([]);
    const nav = useNavigate();


    // Imágenes
    const logoRef = useRef();
    const bannerRef = useRef();
    const [logo, setLogo] = useState('./default-logo.png');
    const [banner, setBanner] = useState('./default-banner.png');


    const listas = (item, list, setList) =>
        setList(l => (l.includes(item) ? l.filter(i => i !== item) : [...l, item]));

    const handleSubmit = async (e) => {
        e.preventDefault();

        const formData = new FormData();
        formData.append("name", nombre);
        formData.append("province", provincia);
        formData.append("population", poblacion);
        formData.append("multi_tenant", multi);
        formData.append("puerto_org", puerto1);
        formData.append("puerto_proc_part", puerto2);
        colSel.forEach(e => formData.append("collaborations[]", e));
        serSel.forEach(i => formData.append("services[]", i));
        formData.append("logo", logoRef.current.files[0]);
        formData.append("banner", bannerRef.current.files[0]);

        try {

            const res = await fetch('http://localhost:4000/councils', {
            method: 'POST',
            body: formData
        });
            if (!res.ok) {
                alert("Error al crear el municipio");
            }
            const data = await res.json();
            const id = data.id;
            const flaskRes = await fetch(`http://localhost:4001/api/crear_instancia`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ id: id})
            });
            
            if (!flaskRes.ok) {
                alert("Municipio creaddo pero error al desplegar la instancia");
            } else {
                alert("Municipio e instancia creados");
            }
            nav('/');
        } catch(error) {
            alert("Error de conexión con el servidor");
        }
    };

    return (
        <div className='council'>
            <h1>Create Council</h1>


            <form onSubmit={handleSubmit}>
                <div className='columna'>
                    <div className='card'>
                        <h2>Describe basic info</h2>
                        <label>Name
                            <br /><input type="text" value={nombre} onChange={e => setNombre(e.target.value)} required />
                        </label>

                        <label>Province
                            <select value={provincia} onChange={e => { SetProvincia(e.target.value), SetPoblacion('') }} required>
                                <option value="">Select</option>{Object.keys(provincias).map(p => (<option key={p}>{p}</option>))}
                            </select>
                        </label>

                        <label>Population
                            <select value={poblacion} onChange={e => SetPoblacion(e.target.value)} disabled={!provincia} required>
                                <option value="">Select</option>
                                {provincias[provincia]?.map(p => (<option key={p}>{p}</option>))}
                            </select>
                        </label>

                        <label>Puerto 1
                            <br /><input type="text" value={puerto1} onChange={e => SetPuerto1(parseInt(e.target.value) || 3001)} required />
                        </label>

                        <label>Puerto 2
                            <br /><input type="text" value={puerto2} onChange={e => SetPuerto2(parseInt(e.target.value) || 3002)} required />
                        </label>

                        <label>
                            <input type="checkbox" checked={multi} onChange={e => setMulti(e.target.checked)} />
                            Multi-Tenant
                        </label>
                    </div>

                    <div className='card'>
                        <h2>Upload images</h2>

                        <button type='button' onClick={() => logoRef.current.click()} >Logo</button>
                        <input ref={logoRef} type='file' accept='image/*' hidden
                            onChange={e => {
                                const f = e.target.files[0];
                                if (f) setLogo(URL.createObjectURL(f));
                            }} /><img src={logo} alt='logo' className='preview logo' /><br />

                        <button type='button' onClick={() => bannerRef.current.click()} >Banner</button>
                        <input ref={bannerRef} type='file' accept='image/*' hidden
                            onChange={e => {
                                const f = e.target.files[0];
                                if (f) setBanner(URL.createObjectURL(f));
                            }} /><img src={banner} alt='banner' className='preview banner' />

                    </div>
                    <br /><br />

                    <div className='card'>
                        <h2>Select collaborations</h2>
                        {colaboraciones.map(c => (<label key={c} className='inline'>
                            <input type="checkbox" checked={colSel.includes(c)}
                                onChange={() => listas(c, colSel, SetColSel)} />
                            {c}
                        </label>))}

                    </div>

                    <div className='card'>
                        <h2>Select services</h2>
                        {servicios.map(c => (<label key={c} className='inline'>
                            <input type="checkbox" checked={serSel.includes(c)}
                                onChange={() => listas(c, serSel, SetSerSel)} />
                            {c}
                        </label>))}

                    </div>



                </div>
                <div className='boton'>
                    <button type='submit' className="btn-primary full">Create</button>
                </div>
            </form>
        </div >
    )

}



export default CreateCouncil;
