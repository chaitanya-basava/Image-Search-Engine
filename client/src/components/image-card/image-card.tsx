import { Link, Typography } from '@mui/material';
import InfoIcon from '@mui/icons-material/Info';
import IconButton from '@mui/material/IconButton';
import ImageListItem from '@mui/material/ImageListItem';
import ImageListItemBar from '@mui/material/ImageListItemBar';

export interface ImageCardProps {
    title: string;
    imgUrl: string;
    userName: string;
    userId: string;
    postedOn: number;
    score: number;
}

/**
 * This component was created using Codux's Default new component template.
 * To create custom component templates, see https://help.codux.com/kb/en/article/kb16522
 */
export const ImageCard = (props: ImageCardProps) => {
    var date = new Date(props.postedOn);
    var subtitleComp = (
        <div>
            by{' '}
            <Link
                color="white"
                variant="overline"
                href={`http://www.flickr.com/people/${props.userId}`}
                target="_blank"
                underline="hover"
            >
                @{props.userName}
            </Link>{' '}
            ({props.score})<br></br>
            {date.toDateString()} {date.toLocaleTimeString()}
        </div>
    );

    var titleComp = (
        <Typography gutterBottom variant="body1" component="div" mt={0}>
            <h4>{props.title}</h4>
        </Typography>
    );

    return (
        <ImageListItem sx={{ maxWidth: 450, height: 250 }}>
            <img
                src={`https://farm66.staticflickr.com/${props.imgUrl}`}
                srcSet={`https://farm66.staticflickr.com/${props.imgUrl}`}
                alt={props.title}
                loading="lazy"
            />
            <ImageListItemBar
                title={titleComp}
                subtitle={subtitleComp}
                actionIcon={
                    <IconButton
                        sx={{ color: 'rgba(255, 255, 255, 0.84)' }}
                        aria-label={`more photos by ${props.userName}`}
                        href={`http://www.flickr.com/photos/${props.userId}`}
                        target="_blank"
                    >
                        <InfoIcon />
                    </IconButton>
                }
            />
        </ImageListItem>
    );
};
