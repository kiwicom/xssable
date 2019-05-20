{% extends "layout.html" %}
{% block body %}
<div class="container">
    <div class="row">
        <div class="col-lg-12 text-left">
            <div class="mt-5">
                <h1> {{ username }}'s blog</h1>
                {% if session['username'] == username %}
                <a href="/blogs/add"><button type="button" class="btn btn-primary">Add blog post</button></a>
                {% endif %}
                <div class="mt-5">
                {% if not blogs %}                
                    <p>Seems like there are no blog posts yet.</p>
                {% else %}
                    {% for blog in blogs %}
                    <h3>
                        {{ blog['title'] }}
                        {% if blog['private'] %}
                        🔒
                        {% endif %}
                    </h3>         
                    <p>{{ blog['body'] }}</p>
                    <div>
                        <span class="badge">Posted {{ blog['timestamp'] }}</span>
                    </div>
                    <hr>
                    {% endfor %}
                {% endif %}
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
