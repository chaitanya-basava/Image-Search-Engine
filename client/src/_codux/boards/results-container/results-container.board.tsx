import { createBoard } from '@wixc3/react-board';
import { ResultsContainer } from '../../../components/results-container/results-container';

const example = [
    {
        title: '2015 Grizzly Bear with Salmon',
        imgUrl: '65535/52891339745_89ee986062_z.jpg',
        userId: '111615580@N03',
        userName: 'Carrie Sapp',
        postedOn: 1683872809000,
        score: 0.12,
    },
    {
        title: 'Cougar Pairi Daiza ED8A5166',
        imgUrl: '65535/52891083268_0948f6d59e_z.jpg',
        userId: 'jakok',
        userName: 'safi kok',
        postedOn: 1683859859000,
        score: 0.09,
    },
    {
        title: 'Pelican Fly-Past',
        imgUrl: '65535/52891311833_b4cf73dc03_z.jpg',
        userId: '34655572@N06',
        userName: 'Chris Ring',
        postedOn: 1683868764000,
        score: 0.0,
    },
];

export default createBoard({
    name: 'ResultsContainer',
    Board: () => <ResultsContainer cards={example} phrase="random" getResults={() => {}} newPhrase={true} />,
    environmentProps: {
        canvasWidth: 1020,
        windowHeight: 839,
        windowWidth: 1222,
    },
});
