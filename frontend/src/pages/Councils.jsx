import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
    FaEye,
    FaSyncAlt,
    FaArrowUp, FaStop,
    FaTrash, FaEdit
} from 'react-icons/fa';
import './CouncilList.css';

function CouncilList() {
    const [rows, setRows] = useState([]);

    const navegar = useNavigate();

    const handleDeploy = async (id) => {
        try {
            const res = await fetch(`http://localhost:4001/deploy/${id}`, {
                method: 'POST',
            });

            if (!res.ok) {
                alert("Error al desplegar el municipio");
            }else{
                alert("Municipio desplegado correctamente");
            }

        } catch (error) {
            console.error("Error al desplegar:", error);
        }
    };

    const handleEdit = (id) => {
        navegar(`/Councils/${id}`);
    };

    // const handleView = (id) => {
    //     navegar(`http:///${id}`);
    // };

    const handleReset = (id) => {
        fetch(`http://localhost:4000/councils/${id}/reset`, {
            method: 'PATCH',
        })
            .then(() => window.location.reload())
            .catch(error => console.error("Error al reiniciar: ", error))
    };

    const handleDestroy = (id) => {
        if (!window.confirm("¿Estas seguro de que quieres eliminar este municipio?")) return;
        fetch(`http://localhost:4000/councils/${id}`, {
            method: 'DELETE',
        })
            .then(() => window.location.reload())
            .catch(error => console.error("Error al desplegar: ", error))
    };

    useEffect(() => {
        fetch('http://localhost:4000/councils', {
            method: 'GET',
        })
            .then(res => res.json())
            .then(data => setRows(data))
            .catch(err => console.error("Error", err))
    }, []);

    return (
        <div className="council-container">
            <h1 className="titulo">Municipios</h1>

            <table className="council-table">
                <thead>
                    <tr>
                        <th>Municipio</th>
                        <th>Multi-tenant</th>
                        <th>Estado</th>
                        <th className='col-lista'>   Colaboraciones   </th>
                        <th className='col-lista'>   Servicios   </th>
                        <th>Ver</th>
                        <th>Resetear</th>
                        <th>Desplegar</th>
                        <th>Modificar</th>
                        <th>Eliminar</th>
                    </tr>
                </thead>
                <tbody>
                    {rows.map(r => (
                        <tr key={r.id}>
                            <td>{r.name}</td>
                            <td>{String(r.multi_tenant)}</td>
                            <td>{r.status}</td>
                            <td className='lista'>{r.collaborations.join(', ')}</td>
                            <td className='lista'>{r.services.join(', ')}</td>
                            <td className="acciones2"><button title="Ver"><FaEye /></button></td>
                            <td className="acciones2"><button title="Refrescar" onClick={() => handleReset(r.id)}><FaSyncAlt /></button></td>
                            <td className="acciones2"><button title={r.status === 'running' ? 'Parar' : 'Desplegar'}
                                onClick={() => handleDeploy(r.id)}>{r.status === 'running' ? <FaStop /> : <FaArrowUp />} </button></td>
                            <td className="acciones2"><button title="Editar" onClick={() => handleEdit(r.id)}><FaEdit /></button></td>
                            <td className="acciones2"><button title="Eliminar" onClick={() => handleDestroy(r.id)} className="danger"><FaTrash /></button></td>

                        </tr>
                    ))}
                </tbody>
            </table>

            <div className='boton'>
                <button className="bot" title="New council" onClick={() => navegar('/CreateCouncil')}>Crear Municipio</button>
            </div>
        </div>
    );
}

export default CouncilList;


