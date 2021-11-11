import * as neo4j from 'neo4j';

function load(user_params) { //var user_params

    var CONFIG = require('./config.json');
    const driver = neo4j.driver(CONFIG.uri,
    neo4j.auth.basic(CONFIG.user, CONFIG.password));

    var graph = {nodes: [], links: []}
    var groups = new Set()
    var link_leaf = new Set()
    var query_1 = '', query_2 = ''
    var type_count = []

   if ((user_params == undefined)) { /*(Object.keys(user_params).length == 0) || */
        query_1 = "MATCH (n) \
        WHERE n.name IN ['Rockets', 'Wizards', 'Lakers', 'Pelicans', 'Bulls', 'Thunder', 'Russell Westbrook', 'Alex Caruso', 'Lonzo Ball'] \
        RETURN id(n), n.name, n.img"

        query_2 = "MATCH (a)-[p]->(b) \
        WHERE b.name IN ['Russell Westbrook', 'Alex Caruso', 'Lonzo Ball'] \
        RETURN id(a), id(b), a.name, b.name"

        //query_1 = 'MATCH(n) RETURN id(n), n.name, n.url'
        //query_2 = 'MATCH (a:Type) -[:RELTYPE]-> (b:Business) RETURN id(a), id(b), a.name, b.name'
    } else if(user_params == 1) { 
        
        //let params = new Map()
        //​params.set('cuisines', ['American']);
        /*var cuisines = {types: 'American'}
        query_1 = 'MATCH (a:Type {name: $types})--> (b:Business) WHERE (a {name: $types})--> (b:Business) RETURN id(b) as id, b.name as name, b.url as url\
        UNION ALL MATCH (n) WHERE n.name = $types RETURN id(n) as id, n.name as name, n.url as url'
        query_2 = 'MATCH (a:Type {name: $types})--> (b:Business) RETURN id(a), id(b), a.name, b.name' */
    }

    var results = driver.session().run(query_1) //cuisines)
    results.subscribe({
        onNext: record => {
            var id = record.get(0).toInt() //.toString()
            const name = record.get(1)
            const url = record.get(2)
            graph.nodes.push({name: name , id: id, url: url, x:100, y: 100}) //, fx: getRndInteger(100, width), fy: getRndInteger(100, 1000)})
        }
    })

    var results = driver.session().run(query_2) //cuisines)
    results.subscribe({
        onNext: record => {
            var team_id = record.get(0).toInt() //.toString()
            var player_id = record.get(1).toInt() //.toString()
            var team = record.get(2)
            var p_name = record.get(3)
            graph.links.push({source: team_id, target: player_id})
            groups.add(team)
            link_leaf.add(p_name)
        }
})
/*
    var query_3 = 'MATCH (b:Type) WHERE (b)-->() RETURN COUNT(b)'
    var results = driver.session().run(query_3)
    results.subscribe({
        onNext: record => {
            var m = record.get(0).toInt()
            type_count.push(m)
        }
    }) 
*/

return {graph, groups, link_leaf};

}
    
