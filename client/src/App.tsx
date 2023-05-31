import React from 'react';
import { Header } from './components/header/header';
import { ResultsContainer } from './components/results-container/results-container';
import { ImageCardProps } from './components/image-card/image-card';

interface AppState {
    cards: Array<ImageCardProps>;
    phrase: string;
    newPhrase: boolean;
}

class App extends React.Component<{}, AppState> {
    constructor(props: {}) {
        super(props);
        this.state = {
            cards: [],
            phrase: '',
            newPhrase: true,
        };
    }

    search = (event: any) => {
        const code = event.keyCode || event.which;
        const phrase = event.target.value;
        if (code === 13 && phrase.length > 2) {
            this.getResults(phrase, true);

            event.target.value = '';
        }
    };

    clearResults = () => {
        this.setState((state) => ({
            cards: [],
            phrase: '',
            newPhrase: true,
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
                <ResultsContainer
                    cards={this.state.cards}
                    phrase={this.state.phrase}
                    getResults={this.getResults}
                    newPhrase={this.state.newPhrase}
                />
            </div>
        );
    }

    getResults = (phrase: string, newPhrase: boolean, page: number = 0, rowsPerPage: number = 10) => {
        fetch('http://localhost:80/text_search', {
            method: 'POST',
            mode: 'cors',
            body: JSON.stringify({
                phrase: phrase,
                page: page,
                rowsPerPage: rowsPerPage,
            }),
            headers: {
                'Content-Type': 'application/json',
            },
        })
            .then((response) => response.json())
            .then((data) => {
                this.setState((state) => ({
                    cards: data.map((i: any) => {
                        return {
                            ...i._source,
                            score: i._score,
                        };
                    }),
                    phrase: phrase,
                    newPhrase: newPhrase,
                }));
            })
            .catch((err) => {
                console.log(err.message);
            });
    };
}

export default App;
