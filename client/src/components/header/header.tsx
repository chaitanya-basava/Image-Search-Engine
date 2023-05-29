import styles from './header.module.scss';
import classNames from 'classnames';

import Box from '@mui/material/Box';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import IconButton from '@mui/material/IconButton';
import GitHubIcon from '@mui/icons-material/GitHub';
import { SearchBar } from '../search-bar/search-bar';

export interface HeaderProps {
    className?: string;
}

/**
 * This component was created using Codux's Default new component template.
 * To create custom component templates, see https://help.codux.com/kb/en/article/kb16522
 */
export const Header = ({ className }: HeaderProps) => {
    return (
        <Box sx={{ flexGrow: 1 }}>
            <AppBar position="static">
                <Toolbar>
                    <Typography
                        variant="h5"
                        noWrap
                        component="div"
                        sx={{ flexGrow: 1, display: { xs: 'none', sm: 'block' } }}
                        align="inherit"
                    >
                        Image Search Demo
                    </Typography>
                    <SearchBar />
                    <Box sx={{ flexGrow: 100 }} />
                    <IconButton
                        aria-label="GitHub"
                        href="https://github.com/chaitanya-basava/Image-Search-Engine"
                        target="_blank"
                        rel="noopener"
                    >
                        <GitHubIcon />
                    </IconButton>
                </Toolbar>
            </AppBar>
        </Box>
    );
};
