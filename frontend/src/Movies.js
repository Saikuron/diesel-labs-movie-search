// Component corresponding to a single movie
function Movie(props) {
    // Get the attributes from the props
    const movie = props.data ? props.data : []
    const movie_name = movie[1]
    const movie_genre = movie[2].split('|')
    const movie_link_imdb = "http://www.imdb.com/title/tt" + movie[4]
    const movie_link_tmdb = "https://www.themoviedb.org/movie/" + movie[5]
    const movie_avg_rating = movie[6]
    const movie_tags = movie[7]
    
    return(
        // Return the movie attributes with a little bit of style
        <div className='Movie'>
            <div>
                <span className='Title'>
                    {movie_name}
                </span>
                <span className="Rating">
                    {Math.round(movie_avg_rating * 10) / 10}
                </span>
            </div>
            <div className="Genres">
                {movie_genre.join(' | ')}
            </div>
            <div>
                <a className="Link" href={movie_link_imdb}>
                    imdb
                </a>
                <a className="Link" href={movie_link_tmdb}>
                    tmdb
                </a>
            </div>
            <div className="Tags">
                {movie_tags.join(' ; ')}
            </div>
        </div>
    );
}

// Component for the list of movies
function Movies(props) {
    // I used help from this link for the searching feature : https://dev.to/salehmubashar/search-bar-in-react-js-545l
    const filteredData = props.data.filter((original_data) => {
        // If input is empty, return full data
        if (props.input === '') {
            return original_data;
        }
        // If input is not empty, return filtered data
        else {
            return original_data[1].toLowerCase().includes(props.input)
        }
    })
    return(
        // Use the Movie Component to show the movies
        <div>
            {filteredData.map((movie,
            idx) => <Movie key={idx} data={movie}/> )}
        </div>
    );
}

export default Movies;