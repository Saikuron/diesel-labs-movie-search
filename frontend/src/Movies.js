import Box from '@mui/material/Box';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import Link from '@mui/material/Link';
import Rating from '@mui/material/Rating';

// Component corresponding to a single movie
function Movie(props) {
    // Get the attributes from the props
    const movie = props.data ? props.data : []
    const movie_name = movie[1]
    const movie_genre = movie[2] ? movie[2].split('|') : [""]
    const movie_link_imdb = "http://www.imdb.com/title/tt" + movie[4]
    const movie_link_tmdb = "https://www.themoviedb.org/movie/" + movie[5]
    const movie_avg_rating = isNaN(movie[6]) ? "NA" : Math.round(movie[6] * 10) / 10
    const movie_tags = movie[7] ? movie[7] : [""]
    
    return(
        // Return the movie attributes with a little bit of style
            <Card sx={{ minWidth: 400, maxWidth: 500, backgroundColor: "#999999", margin: "1%" }}>
                <CardContent>
                    <Typography variant="h5" component="div">
                        {movie_name}
                    </Typography>
                    <Rating value={movie_avg_rating} precision={0.1} readOnly />
                    <Typography sx={{ mb: 1.5 }} color="text.secondary">
                        {movie_genre.join(' | ')}
                    </Typography>
                    <Typography variant="body2">
                        <Link sx = {{ margin: "2%" }} underline="hover" href={movie_link_imdb}>imdb</Link>
                        <Link sx = {{ margin: "2%" }} underline="hover" href={movie_link_tmdb}>tmdb</Link>
                    </Typography>
                    <Typography variant="body2">
                        {movie_tags.join(' ; ')}
                    </Typography>
                </CardContent>
            </Card>
    );
}

// Component for the list of movies
function Movies(props) {
    const moviesToShow = props.filteredData ? props.filteredData.map((movie, idx) => <Movie key={idx} data={movie}/> ) : "Nothing"
    return(
        // Use the Movie Component to show the movies received from the parent Component
        <div>
            {moviesToShow}
        </div>
    );
}

export default Movies;