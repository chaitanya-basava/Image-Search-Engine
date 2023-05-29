import { Header } from './components/header/header';
import { ResultsContainer } from './components/results-container/results-container';

var example = [
    {
        title: '2015 Grizzly Bear with Salmon',
        imgUrl: '65535/52891339745_89ee986062_z.jpg',
        userId: '111615580@N03',
        userName: 'Carrie Sapp',
        postedOn: 1683872809000,
    },
    {
        title: 'Cougar Pairi Daiza ED8A5166',
        imgUrl: '65535/52891083268_0948f6d59e_z.jpg',
        userId: 'jakok',
        userName: 'safi kok',
        postedOn: 1683859859000,
    },
    {
        title: 'Pelican Fly-Past',
        imgUrl: '65535/52891311833_b4cf73dc03_z.jpg',
        userId: '34655572@N06',
        userName: 'Chris Ring',
        postedOn: 1683868764000,
    },
    {
        title: '2015 Grizzly Bear with Salmon',
        imgUrl: '65535/52891339745_89ee986062_z.jpg',
        userId: '111615580@N03a',
        userName: 'Carrie Sapp',
        postedOn: 1683872809000,
    },
    {
        title: 'Cougar Pairi Daiza ED8A5166',
        imgUrl: '65535/52891083268_0948f6d59e_z.jpg',
        userId: 'jakoka',
        userName: 'safi kok',
        postedOn: 1683859859000,
    },
    {
        title: 'Pelican Fly-Past',
        imgUrl: '65535/52891311833_b4cf73dc03_z.jpg',
        userId: '34655572@N06a',
        userName: 'Chris Ring',
        postedOn: 1683868764000,
    },
];

function App() {
    return (
        <div>
            <Header />
            <ResultsContainer cards={example} />
        </div>
    );
}

export default App;
