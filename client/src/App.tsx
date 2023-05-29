import styles from './App.module.scss';
import { Header } from './components/header/header';
import Classnames from 'classnames';
import Header_module from './components/header/header.module.scss';
import { ImageCard } from './components/image-card/image-card';

function App() {
    return (
        <div className={styles.App}>
            <Header />
            {/* <ImageCard /> */}
        </div>
    );
}

export default App;
