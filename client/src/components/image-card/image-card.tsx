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
}

/**
 * This component was created using Codux's Default new component template.
 * To create custom component templates, see https://help.codux.com/kb/en/article/kb16522
 */
export const ImageCard = (props: ImageCardProps) => {
    var date = new Date(props.postedOn);
    var subtitleComp = (
        <div>
            by <Link color="white" variant="overline" href={`http://www.flickr.com/people/${props.userId}`} underline="hover">
                @{props.userName}
            </Link>
            <br></br>
            {date.toDateString()} {date.toLocaleTimeString()}
        </div>
    )

    var titleComp = (
        <Typography gutterBottom variant="h4" component="div">
            {props.title}
        </Typography>
    )

    return (
        <ImageListItem key={props.imgUrl}>
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
              >
                <InfoIcon />
              </IconButton>
            }
          />
        </ImageListItem>
    );
};
