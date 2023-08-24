# imdb_extractor
Script de extração dos filmes/séries mais populares ou melhores segundo o IMDB.

O script original continha, basicamente, funções. Transformei essas funções
em uma classe - IMDB_extractor.

Além disso, adicionei dois parâmetros:
	1) top_num: permite escolher o número máximo de filmes da extração;
	2) content_type: permite escolher entre filmes ou séries, e entre os mais populares ou entre os melhores.
			 content_types válidos: 'popular movies', 'popular series', 'best movies', 'best series'
