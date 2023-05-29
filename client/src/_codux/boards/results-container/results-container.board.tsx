import { createBoard } from '@wixc3/react-board';
import { ResultsContainer } from '../../../components/results-container/results-container';

export default createBoard({
    name: 'ResultsContainer',
    Board: () => <ResultsContainer />,
    environmentProps: {
        canvasWidth: 314,
    },
});
