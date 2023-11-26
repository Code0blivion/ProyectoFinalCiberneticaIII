'use client'
import { useSearchParams } from 'next/navigation'

export default function Page() {
  const searchParams = useSearchParams();
  const numVariables = parseInt(searchParams.get('numVariables'));
  const numRestricciones = parseInt(searchParams.get('numRestricciones'));

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
      console.log('Success:', data);
    })
    .catch((error) => {
      console.error('Error:', error);
    });
  };

  return (
    <div>
      <p>Número de variables: {numVariables}</p>
      <p>Número de restricciones: {numRestricciones}</p>
      <p>Ingresa tu función objetivo y tus restricciones</p>
      <form onSubmit={handleSubmit} className="flex-container">
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
    </div>
  )
}

