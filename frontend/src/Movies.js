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
        <div className='Movie'>
            <div>
                <span className='Title'>
                    {movie_name}
                </span>
                <span className="Rating">
                    {movie_avg_rating}
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
    const moviesToShow = props.filteredData ? props.filteredData.map((movie, idx) => <Movie key={idx} data={movie}/> ) : "Nothing"
    return(
        // Use the Movie Component to show the movies received from the parent Component
        <div>
            {moviesToShow}
        </div>
    );
}

export default Movies;