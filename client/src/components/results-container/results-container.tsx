import * as React from 'react';
import ManageSearchIcon from '@mui/icons-material/ManageSearch';
import { ImageCard, ImageCardProps } from '../image-card/image-card';
import { TablePagination, useMediaQuery, useTheme, Grid, ImageList, ImageListItem, ListSubheader } from '@mui/material';

interface ResultsProps {
    cards: Array<ImageCardProps>;
    phrase: string;
    getResults: Function;
    newPhrase: boolean;
}

export function ResultsContainer(props: ResultsProps) {
    const theme = useTheme();
    const isLarge = useMediaQuery(theme.breakpoints.up('lg'));
    const isExtraLarge = useMediaQuery(theme.breakpoints.up('xl'));

    const [page, setPage] = React.useState(0);
    const [rowsPerPage, setRowsPerPage] = React.useState(10);

    const handleChangePage = (
        event: React.MouseEvent<HTMLButtonElement> | null,
        newPage: number
    ) => {
        setPage(newPage);

        props.getResults(props.phrase, false, newPage, rowsPerPage);
    };

    const handleChangeRowsPerPage = (
        event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
    ) => {
        const newRowsPerPage = parseInt(event.target.value, 10);
        setRowsPerPage(newRowsPerPage);
        setPage(0);

        props.getResults(props.phrase, false, 0, newRowsPerPage);
    };

    if (props.cards.length === 0) {
        if (page !== 0 || rowsPerPage !== 10) {
            setRowsPerPage(10);
            setPage(0);
        }

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
        if (props.newPhrase && (page !== 0 || rowsPerPage !== 10)) {
            setRowsPerPage(10);
            setPage(0);
        }
        
        let numCols = 1;

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
                    <ImageListItem key="pagination" cols={numCols}>
                        <ListSubheader
                            sx={{
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                            }}
                        >
                            <TablePagination
                                component="div"
                                count={100}
                                page={page}
                                onPageChange={handleChangePage}
                                rowsPerPage={rowsPerPage}
                                onRowsPerPageChange={handleChangeRowsPerPage}
                            />
                        </ListSubheader>
                    </ImageListItem>
                </ImageList>
            </Grid>
        );
    }
}
