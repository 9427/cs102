<!DOCTYPE html>
<html>
    <head>
        <link rel="stylesheet" href="//cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.2.12/semantic.min.css"></link>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.2.12/semantic.min.js"></script>
    </head>
    <body>
        <div class="ui container" style="padding-top: 10px;">
        <table class="ui celled table">
            <thead>
                <th>Title</th>
                <th>Author</th>
                <th>#Likes</th>
                <th>#Comments</th>
                <th colspan="5">Label</th>
            </thead>
            <tbody>
                %for row in rows:
                <tr>
                    <td><a href="{{ row.url }}">{{ row.title }}</a></td>
                    <td>{{ row.author }}</td>
                    <td>{{ row.points }}</td>
                    <td>{{ row.comments }}</td>
                    <td class="mark_1"><a href="/add_label/?label=1&id={{ row.id }}">1</a></td>
                    <td class="mark_2"><a href="/add_label/?label=2&id={{ row.id }}">2</a></td>
                    <td class="mark_3"><a href="/add_label/?label=3&id={{ row.id }}">3</a></td>
                    <td class="mark_4"><a href="/add_label/?label=4&id={{ row.id }}">4</a></td>
                    <td class="mark_5"><a href="/add_label/?label=5&id={{ row.id }}">5</a></td>
                </tr>
                %end
            </tbody>
            <tfoot class="full-width">
                <tr>
                    <th colspan="7">
                        <a href="/update" class="ui right floated small primary button">this button does its best to update the database, be gentle with it</a>
                    </th>
                </tr>
            </tfoot>
        </table>
        </div>
    </body>
</html>
