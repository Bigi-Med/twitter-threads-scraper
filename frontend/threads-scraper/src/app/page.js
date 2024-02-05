'use client'
import React, { useState } from 'react'
import styles from "./page.module.css"
const URL = "http://localhost:5000/?profile="
export default function Home() {

  const getThreads = async (profile) => {
    const fullUrl = URL + profile
    const response = await fetch(fullUrl)
    console.log(response);
  }

  const [profile, setProfile] = useState('')
  const profiles = [
    { label: 'Select a profile', value: '' },
    { label: 'Alex hormozi', value: '@hormozi' },
    { label: 'Grant Cardone', value: '@grantcardone' },
    { label: 'garyvee', value: '@garyvee' },
    { label: 'Tim Tebow', value: '@timtebow' },
    { label: 'Codie Sanchez', value: '@codiesanchez' },
    { label: 'Ryan Pineda', value: '@ryanpineda' },
    { label: 'Ed Mylett', value: '@edmylett' },
    { label: 'Elena Cardone', value: '@elenacardone' },
  ]
  const handleDropdownChange = (event) => {
    setProfile(event.target.value);
  };

  return (
    <div className={styles.pageContainer}>
      <h1 className={styles.title}>Threads profile scraper</h1>
      <div className={styles.pageBody}>
        <div className={styles.profileList}>
          <div className={styles.dropDownArrow}>
            <select id={styles.dynamicDropdown} onChange={handleDropdownChange} className={styles.dropdown}>
              {profiles.map((option, index) => (
                <option key={index} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </div>
        </div>
        <div className={styles.buttonContainer}>
          <button onClick={() => getThreads(profile)}>Get Threads</button>
        </div>
      </div>
    </div>
  )
}
