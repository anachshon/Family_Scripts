{
    e_step <- function( x, nb )
    {
        nof_pos = length( x )
        nb_nof_zeros = nof_pos * dnbinom( 0, mu = nb[ "mu" ], size = nb[ "size" ] )
        curr_drop = ( sum( x == 0 ) - nb_nof_zeros ) / nof_pos
        curr_drop = max( 0, curr_drop )
        return( curr_drop )
    }

    nb_ml <- function( v )
    {
        nb = fitdistr( v, densfun = "negative binomial" )
        return( nb$estimate )
    }
    
    m_step <- function( x, curr_drop )
    {
        nof_pos = length( x )
        y = x[ order( x ) ]
        drop_nof_zeros = as.integer( nof_pos * curr_drop )
        nof_zeros = sum( y == 0 )
        if ( nof_zeros > drop_nof_zeros )
            y = y[ ( drop_nof_zeros + 1 ) : nof_pos ]
        return( nb_ml( y ) )
    }
    
    lik_pos <- function( value, curr_drop, nb )
    {
        p = ( value == 0 ) * curr_drop + ( 1 - curr_drop ) * dnbinom( value, mu = nb[ "mu" ], size =  nb[ "size" ] )
        return( -log10( p ) )
    }
    
    lik_all <- function( x_table, curr_drop, nb )
    {
        return( sum ( x_table * lik_pos( as.numeric( names( x_table ) ), curr_drop, nb ) ) )
    }
}


{
    EM <- function( x, nof_start_points, nof_iterations )
    {
        best_lik = 1e100
        nof_pos = length( x )
        x_table = table( x )
        for ( m in 1 : nof_start_points )
        {
            curr_drop = runif( 1, 0, 1 ) * sum( x == 0 ) / nof_pos
            nb = m_step( x, curr_drop )
    
            for ( n in 1 : nof_iterations )
            {
                curr_drop = e_step( x, nb )
                nb = m_step( x, curr_drop )
                curr_lik = lik_all( x_table, curr_drop, nb )
                if ( curr_lik < best_lik )
                {
                    best_drop = curr_drop
                    best_mu = nb[ "mu" ]
                    best_size = nb[ "size" ]
                    best_lik = curr_lik
                }
            }
        }
        ret_vals = c( best_drop, best_mu, best_size, best_lik )
        names( ret_vals ) = c( "drop", "mu", "size", "likelihood" )
        return( ret_vals )
    }
}

