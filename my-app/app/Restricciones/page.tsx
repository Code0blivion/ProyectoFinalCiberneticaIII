'use client'
import { useSearchParams } from 'next/navigation'
import styles from './page.module.css'
import React, { useState, useRef, useEffect} from "react";

export default function Page() {
  const searchParams = useSearchParams();
  const numVariables = parseInt(searchParams.get('numVariables'));
  const numRestricciones = parseInt(searchParams.get('numRestricciones'));
  const [tabla, setTabla] = useState(<div></div>);
  const [resultados,setResultados] = useState(<div></div>)

  const handleSubmit = (e) => {
    e.preventDefault();

    const zValues = Array.from({ length: numVariables }).map((_, i) => 
      parseFloat(document.getElementById(`input-z-${i}`).value)
    );

    const constraintValues = Array.from({ length: numRestricciones }).map((_, i) => 
      Array.from({ length: numVariables }).map((_, j) => 
        parseFloat(document.getElementById(`input-${i}-${j}`).value)
      )
    );

    const selectValues = Array.from({ length: numRestricciones }).map((_, i) => 
      document.getElementById(`select-${i}`).value
    );

    const lastInputValues = Array.from({ length: numRestricciones }).map((_, i) => 
      parseFloat(document.getElementById(`input-number-${i}`).value)
    );

    const data = {
      zValues,
      constraintValues,
      selectValues,
      lastInputValues
    };
    fetch('http://localhost:5000/simplex_api/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
      data['cabecera'].push('R')
      var cabecera=(
        <tr>
        <th scope="row">~</th>
        {data['cabecera'].map((i)=>(<th>{i}</th>))}
      </tr>
      )

      setTabla(<div>
        {data['matrices'].map((matriz)=>(
          <table>
            {cabecera}
            {matriz.map((fila)=>(
                <tr>
                  {<th>{fila.shift()}</th>}
                  {fila.map(( i )=>(
                    <td>{i}</td>
                  )
                  )}
                </tr>
            )
            )}
          </table>
        ))}
      </div>)

      setResultados(
        <ol>
          {data['resultados'].map((v)=>(
            <li>{v[0]} = {v[1]}</li>
        ))}
        </ol>
      )

    })
    .catch((error) => {
      console.error('Error:', error);
    });
  };

  return (
    <div className={styles.container}>
      <p>Número de variables: {numVariables}</p>
      <p>Número de restricciones: {numRestricciones}</p>
      <p>Ingresa tu función objetivo y tus restricciones</p>
      <form onSubmit={handleSubmit} className={styles.flex_container}>
        <div className="flex-row">
          <span>Z = </span>
          {Array.from({ length: numVariables }).map((_, i) => (
            <div key={i} className="label-container">
              <input type="number" id={`input-z-${i}`} name={`z-${i}`} className="input-number" />
              <span>X<sub>{i + 1}</sub></span>
            </div>
          ))}
        </div>
        {Array.from({ length: numRestricciones }).map((_, i) => (
          <div key={i} className="flex-row">
            {Array.from({ length: numVariables }).map((_, j) => (
              <div key={j} className="label-container">
                <input type="number" id={`input-${i}-${j}`} name={`x-${i}-${j}`} className="input-number" />
                <span>X<sub>{j + 1}</sub></span>
              </div>
            ))}
            <select id={`select-${i}`} name={`select-${i}`}>
              <option value="=">=</option>
              <option value=">=">≥</option>
              <option value="<=">≤</option>
            </select>
            <input type="number" id={`input-number-${i}`} name={`number-${i}`} className="input-number" />
          </div>
        ))}
        <button type="submit" className="submit-button">Resolver</button>
      </form>
      <div className={styles.resultadosmatrices}>{tabla}</div>
      <div className={styles.resultados}>{resultados}</div>
    </div>
  )
}

