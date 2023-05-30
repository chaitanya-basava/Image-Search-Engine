import { Grid, ImageList, ImageListItem, ListItemText, ListSubheader } from '@mui/material';
import { useMediaQuery, useTheme } from '@mui/material';
import ManageSearchIcon from '@mui/icons-material/ManageSearch';
import { ImageCard, ImageCardProps } from '../image-card/image-card';

interface ResultsProps {
    cards: Array<ImageCardProps>;
    phrase: string;
}

export function ResultsContainer(props: ResultsProps) {
    const theme = useTheme();
    const isLarge = useMediaQuery(theme.breakpoints.up('lg'));
    const isExtraLarge = useMediaQuery(theme.breakpoints.up('xl'));

    if (props.cards.length === 0) {
        return (
            <Grid
                container
                spacing={0}
                direction="column"
                alignItems="center"
                justifyContent="center"
                sx={{
                    minHeight: '100vh',
                }}
            >
                <ManageSearchIcon />
                search for results
            </Grid>
        );
    } else {
        var numCols = 1;

        if (isExtraLarge) numCols = 3;
        else if (isLarge) numCols = 2;

        return (
            <Grid
                container
                spacing={0}
                direction="column"
                alignItems="center"
                justifyContent="center"
                sx={{
                    minHeight: '100vh',
                }}
            >
                <ImageList cols={numCols}>
                    <ImageListItem key="Subheader" cols={numCols}>
                        <ListSubheader
                            sx={{
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                            }}
                        >
                            <h1>Search results for: {props.phrase}</h1>
                        </ListSubheader>
                    </ImageListItem>
                    {props.cards.map((item) => (
                        <ImageCard
                            key={`${item.imgUrl}-${item.userId}`}
                            title={item.title}
                            imgUrl={item.imgUrl}
                            userName={item.userName}
                            userId={item.userId}
                            postedOn={item.postedOn}
                            score={item.score}
                        />
                    ))}
                </ImageList>
            </Grid>
        );
    }
}
