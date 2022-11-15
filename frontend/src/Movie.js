
function Movie(props) {
    const movie = props.data ? props.data : []
    const movie_id = movie[0]
    const movie_name = movie[1]
    const movie_genre = movie[2].split('|')
    const movie_link_imdb = "http://www.imdb.com/title/tt" + movie[4]
    const movie_link_tmdb = "https://www.themoviedb.org/movie/" + movie[5]
    const movie_avg_rating = movie[6]
    const movie_tags = movie[7]
    
    return(
        <div className='Movie'>
            <div>
                <span className='Title'>
                    {movie_id} - {movie_name}
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
        // <div key={props.key}>{movie[0]} {movie[1]} {movie[2]} {movie[3]} {movie[4]} {movie[5]} {movie[6]}</div>
    );
}

export default Movie;