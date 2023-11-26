'use client'
import Image from 'next/image'
import styles from './page.module.css'
import {useState} from 'react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'

export default function Home() {
  const router = useRouter();
  const [numVariables, setNumVariables] = useState("");
  const [numRestricciones, setNumRestricciones] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    router.push(`/Restricciones/?numVariables=${numVariables}&numRestricciones=${numRestricciones}`);
  };

  return (
    <main className={styles.main}>
      <h1>Solucionador de PL</h1>
      <p>Esta aplicación permite utilizar herramientas de PL para minimizar una ecuación objetivo.</p>
      <form className={styles.seleccion} onSubmit={handleSubmit}>
        <label>Numero de variables</label>
        <input type="number" value={numVariables} onChange={(e) => setNumVariables(e.target.value)} />
        <label>Numero de restricciones</label>
        <input type="number" value={numRestricciones} onChange={(e) => setNumRestricciones(e.target.value)} />
        <button type="submit">ACEPTAR</button>
      </form>
    </main>
  )
}
