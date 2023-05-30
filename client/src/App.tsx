import React from 'react';
        import { Header } from './components/header/header';
        import { ResultsContainer } from './components/results-container/results-container';
        import { ImageCardProps } from './components/image-card/image-card';

        interface AppState {
        cards: Array
<ImageCardProps>;
    phrase: string;
    }

    class App extends React.Component<{}, AppState> {
    constructor(props: {}) {
    super(props);
    this.state = {
    cards: [],
    phrase: "",
    };
    }

    search = (event: any) => {
    var code = event.keyCode || event.which;
    var phrase = event.target.value;
    if (code === 13 && phrase.length > 2) {
    fetch('http://localhost:80/text_search', {
    method: "POST",
    mode: "cors",
    body: JSON.stringify({
    phrase: phrase
    }),
    headers: {
    "Content-Type": "application/json",
    }
    })
    .then(response => response.json())
    .then(data => {
    this.setState((state) => ({
    cards: data.map(
    (i: any) => {
    return {
    ...i._source,
    score: i._score
    }
    }
    ),
    phrase: phrase
    }));
    })
    .catch((err) => {
    console.log(err.message);
    });

    event.target.value = '';
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
        <ResultsContainer cards={this.state.cards} phrase={this.state.phrase} />
    </div>
    );
    }
    }

    export default App;
