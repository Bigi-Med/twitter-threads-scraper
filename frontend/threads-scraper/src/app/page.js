'use client'
import React, { useState } from 'react'
import styles from "./page.module.css"
const URL = "http://localhost:5000/?profile="
export default function Home() {
 const [profile, setProfile] = useState('')
 const [loading, setLoading] = useState(false)

const downloadThreads = (file) => {
  console.log('downloading .....')
  const fileName = 'data.json'
  const jsonStr = JSON.stringify(file,null,2)

  let element = document.createElement('a')
  element.setAttribute('href','data:text/plain;charset=utf-8,' + encodeURIComponent(jsonStr))
  element.setAttribute('download',fileName)
  element.style.display = 'none'
  document.body.appendChild(element)
  element.click()
  document.body.removeChild(element)
}

const parseData = (data) => {
  let parsedData = []
  console.log(data)
  data.forEach(element => { parsedData.push(element.text)
  });
  const cleanQuotes = parsedData.map((quote, index) => ({
    id: index,
    text: quote.replace(/\n/g, ' ') // Replace all newline characters with a space
  }));
  return cleanQuotes;
}

const getThreads = async (profile) => {
  if(profile === ''){
    console.log("You must choose a profile to scrape")
  } else{
    setLoading(true)
    console.log("getting threads")
    const fullUrl = URL + profile
    const response = await fetch(fullUrl)
    const data = await response.json()
    setLoading(false)
    const parsedData = parseData(data[0].thread)
    console.log(parsedData);
    downloadThreads(parsedData)
    }
  }

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
          <button onClick={() => getThreads(profile)} className={styles.getThreads}>Get Threads</button>
        </div>
      </div>
      <div className={styles.loadingContainer}>
        {loading && (
          <div className={styles.loadingDiv}>
            <img src="/assets/Dual-Ring-removebg.png" className={styles.loadingIcon} alt="Loading" />
          </div>
        )}
      </div>
    </div>
  )
}
