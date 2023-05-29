import styles from './App.module.scss';
import { Header } from './components/header/header';
import { ResultsContainer } from './components/results-container/results-container';

function App() {
    return (
        <div className={styles.App}>
            <Header />
            <ResultsContainer />
        </div>
    );
}

export default App;
