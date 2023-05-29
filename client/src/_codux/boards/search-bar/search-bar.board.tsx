import { createBoard } from '@wixc3/react-board';
import { SearchBar } from '../../../components/search-bar/search-bar';

export default createBoard({
    name: 'SearchBar',
    Board: () => <SearchBar />
});
