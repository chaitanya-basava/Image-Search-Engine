import React from 'react';
import { Header } from './components/header/header';
import { ResultsContainer } from './components/results-container/results-container';
import { ImageCardProps } from './components/image-card/image-card';

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

interface AppState {
    cards: Array<ImageCardProps>;
}

class App extends React.Component<{}, AppState> {
    constructor(props: {}) {
        super(props);
        this.state = {
            cards: [],
        };
    }

    search = (event: any) => {
        var code = event.keyCode || event.which;
        var phrase = event.target.value;
        if (code === 13 && phrase.length > 2) {
            alert(phrase);
            event.target.value = '';
            this.setState((state) => ({
                cards: example,
            }));
        }
    };

    clearResults = () => {
        this.setState((state) => ({
            cards: [],
        }));
    };

    render(): React.ReactNode {
        return (
            <div>
                <Header
                    search={this.search}
                    clear={this.clearResults}
                    displayClear={this.state.cards.length !== 0}
                />
                <ResultsContainer cards={this.state.cards} />
            </div>
        );
    }
}

export default App;
