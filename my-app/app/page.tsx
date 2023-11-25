'use client'
import Image from 'next/image'
import styles from './page.module.css'
import {useState} from 'react'

export default function Home() {
  const [nombre, setNombre] = useState("");
  return (
    <main className={styles.main}>
      <h1>Solucionador de PL</h1>
      <p>Esta aplicación permite utilizar herramientas de PL para minimizar una ecuación objetivo.</p>
      <form className={styles.seleccion}>
        <label>Numero de variables</label><input type="number"></input>
        <label>Numero de restricciones</label><input type="number"></input>
        <button>ACEPTAR</button>
      </form>
    </main>
  )
}
