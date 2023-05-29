import Box from '@mui/material/Box';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import IconButton from '@mui/material/IconButton';
import GitHubIcon from '@mui/icons-material/GitHub';
import { SearchBar } from '../search-bar/search-bar';
import LinkedInIcon from '@mui/icons-material/LinkedIn';

/**
 * This component was created using Codux's Default new component template.
 * To create custom component templates, see https://help.codux.com/kb/en/article/kb16522
 */
export const Header = () => {
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
                        paddingRight={5}
                    >
                        Image Search
                    </Typography>
                    <SearchBar />
                    <IconButton
                        aria-label="LinkedIn"
                        href="https://www.linkedin.com/in/basava-sai-naga-viswa-chaitanya-665083172/"
                        target="_blank"
                        rel="noopener"
                    >
                        <LinkedInIcon />
                    </IconButton>
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
