import styles from "./profile.module.css"
export default function Profile({ label, options, onChange }){
return (
    <div className={styles.dropDownArrow}>
      <select id={styles.dynamicDropdown} onChange={onChange} className={styles.dropdown}>      
        {options.map((option, index) => (
          <option key={index} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
    </div>
  );
}