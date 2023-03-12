<!DOCTYPE html>
<html>

<head>
    <title>Bootstrap Typeahead Example</title>
    <link rel="stylesheet" type="text/css"
        href="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.5.2/css/bootstrap.min.css">
    <script type="text/javascript" src="https://code.jquery.com/jquery-3.5.1.min.js"></script>
    <script type="text/javascript"
        src="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.5.2/js/bootstrap.bundle.min.js"></script>
    <script type="text/javascript"
        src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-3-typeahead/4.0.2/bootstrap3-typeahead.min.js"></script>
</head>

<body>
    <div class="container mt-5">
        <h3>Bootstrap Typeahead Example</h3>
        <input type="text" id="searchInput" class="form-control typeahead" placeholder="Enter a keyword">
    </div>

    <script type="text/javascript">
        var keywords = ["Apple", "Banana", "Cherry", "Durian", "Elderberry", "Fig", "Grape", "Honeydew", "Jackfruit", "Kiwi"];
        $('#searchInput').typeahead({
            source: keywords
        });
    </script>
</body>

</html>
