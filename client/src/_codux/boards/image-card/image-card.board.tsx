import { createBoard } from '@wixc3/react-board';
import { ImageCard } from '../../../components/image-card/image-card';

var example = {
    title: '2015 Grizzly Bear with Salmon ',
    imgUrl: '65535/52891339745_89ee986062_z.jpg',
    userId: '111615580@N03',
    userName: 'Carrie Sapp',
    postedOn: 1683872809000,
    score: 0.12,
};

export default createBoard({
    name: 'ImageCard',
    Board: () => (
        <ImageCard
            title={example.title}
            imgUrl={example.imgUrl}
            userName={example.userName}
            userId={example.userId}
            postedOn={example.postedOn}
            score={example.score}
        />
    ),
});
