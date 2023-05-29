import Card from '@mui/material/Card';
import CardMedia from '@mui/material/CardMedia';
import Typography from '@mui/material/Typography';
import CardContent from '@mui/material/CardContent';
import { Button, CardActionArea, CardActions } from '@mui/material';

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
    return (
        <Card sx={{ maxWidth: 345, height: 525 }}>
            <CardActionArea>
                <CardMedia
                    component="img"
                    height="300"
                    image={`https://farm66.staticflickr.com/${props.imgUrl}`}
                    alt="flickr image"
                />
                <CardContent>
                    <Typography gutterBottom variant="h4" component="div">
                        {props.title}
                    </Typography>
                    <Typography variant="button" color="text.secondary">
                        Image captured by {props.userName}.
                        <br></br>
                        {date.toDateString()} {date.toLocaleTimeString()}
                        <br></br>
                    </Typography>
                </CardContent>
            </CardActionArea>
            <CardActions>
                <Button size="small" color="primary" href={`http://www.flickr.com/people/${props.userId}`}>
                    Profile
                </Button>
                <Button size="small" color="primary" href={`http://www.flickr.com/photos/${props.userId}`}>
                    Photos
                </Button>
            </CardActions>
        </Card>
    );
};
