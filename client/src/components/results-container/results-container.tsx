import { ImageCardProps } from "../image-card/image-card";

import { Grid } from "@mui/material";
import React, { Component } from "react";
import ManageSearchIcon from '@mui/icons-material/ManageSearch';

interface ResultsProps {

}

interface ResultsState {
    cards: Array<ImageCardProps>
}

export class ResultsContainer extends Component<ResultsProps, ResultsState> {
    constructor(props: ResultsProps) {
        super(props);
        this.state = {
            cards: []
        }
    }

    render(): React.ReactNode {
        if(this.state.cards?.length === 0) {
            return (
                <Grid
                    container
                    spacing={0}
                    direction="column"
                    alignItems="center"
                    justifyContent="center"
                    sx={{
                        minHeight: '100vh'
                    }}
                >
                    <ManageSearchIcon />
                    search for results
                </Grid>
            );
        } else {
            return (
                <Grid container spacing={{ xs: 2, md: 3 }} columns={{ xs: 4, sm: 8, md: 12 }}>
                
                </Grid>
            );
        }
    }
}
