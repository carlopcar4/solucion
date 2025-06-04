import { useParams } from "react-router-dom";
import { useRef, useEffect, useState } from 'react';
import { useNavigate } from "react-router-dom";
import './CouncilList.css'


function ContentCouncil() {
    const { id } = useParams()

    const [caract, setCaract] = useState({});
    const [nombre, setNombre] = useState('');
    const [provincia, SetProvincia] = useState('');
    const [poblacion, SetPoblacion] = useState('');
    const [puerto1, SetPuerto1] = useState(3001);
    const [puerto2, SetPuerto2] = useState(3002);
    const [multi, setMulti] = useState(false);
    const [colSel, SetColSel] = useState([]);
    const [serSel, SetSerSel] = useState([]);
    const nav = useNavigate();
    const logoRef = useRef();
    const bannerRef = useRef();
    const [logo, setLogo] = useState('');
    const [banner, setBanner] = useState('');


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

    useEffect(() => {
        fetch(`http://localhost:4000/councils/${id}`, {
            method: 'GET',
        })
            .then(res => res.json())
            .then(c => setCaract(c))
            .catch(er => console.error("Error", er))
    }, [id]);

    useEffect(() => {
        if (Object.keys(caract).length > 0) {
            setNombre(caract.name || '')
            SetProvincia(caract.province || '')
            SetPoblacion(caract.population || '')
            SetPuerto1(caract.puerto_org || 3001)
            SetPuerto2(caract.puerto_proc_part || 3002)
            setMulti(caract.multi_tenant || false)
            SetColSel(caract.collaborations || [])
            SetSerSel(caract.services || [])
            setLogo(caract.logo_url || './default-logo.png')
            setBanner(caract.banner_url || './default-banner.png')
        }
    }, [caract])


    const listas = (item, list, setList) =>
        setList(l => (l.includes(item) ? l.filter(i => i !== item) : [...l, item]));

    const handleSubmit = e => {
        e.preventDefault();

        const formData = new FormData();
        colSel.forEach(e => formData.append("collaborations[]", e));
        serSel.forEach(i => formData.append("services[]", i));

        fetch(`http://localhost:4000/councils/${id}`, {
            method: 'PATCH',
            body: formData
        })
            .then(res => {
                if (res.ok) {
                    alert('Municipio modificado correctamente');
                    nav('/')
                } else if (res.status === 204) {
                    nav('/')
                } else {
                    alert("Error al modificar el municipio")
                }
            })
            .catch(() => alert("Error de conexión con el servidor"));
    };

    return (
        <div className="council">
            <h1>Modified information of {caract.name}</h1>

            <form onSubmit={handleSubmit}>
                <div className='columna'>

                    <div className="card">
                        <h2>basic information</h2>
                        <label>Name
                            <br /><input type="text" defaultValue={nombre} readOnly/>
                        </label>

                        <label>Province
                            <br /><input type="text" defaultValue={provincia} readOnly/>
                        </label>

                        <label>Population
                            <br /><input type="text" defaultValue={poblacion} readOnly/>
                        </label>

                        <label>Puerto 1
                            <br /><input type="text" defaultValue={puerto1} readOnly/>
                        </label>

                        <label>Puerto 2
                            <br /><input type="text" defaultValue={puerto2} readOnly/>
                        </label>

                        <label>
                            <input type="checkbox" defaultChecked={multi} readOnly/>
                            Multi-Tenant
                        </label>
                    </div>

                    <div className='card'>
                        <h2>Logo</h2>
                        <input ref={logoRef} type='file' accept='image/*' hidden
                            onChange={e => {
                                const f = e.target.files[0];
                                if (f) setLogo(URL.createObjectURL(f));
                            }} />{logo && <img src={logo} alt='logo' className='preview logo' />}<br />

                        <h2>Banner</h2>
                        <input ref={bannerRef} type='file' accept='image/*' hidden
                            onChange={e => {
                                const f = e.target.files[0];
                                if (f) setBanner(URL.createObjectURL(f));
                            }} />{banner && <img src={banner} alt='banner' className='preview banner' />}

                    </div>
                    <br /><br />

                    <div className='card'>
                        <h2>collaborations</h2>
                        {colaboraciones.map(c => (<label key={c} className='inline'>
                            <input type="checkbox" checked={colSel.includes(c)}
                                onChange={() => listas(c, colSel, SetColSel)} />
                            {c}
                        </label>))}
                    </div>

                    <div className='card'>
                        <h2>services</h2>
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
        </div>
    )
}

export default ContentCouncil;