import pytest


def test_root_redirect(client):
    """Test that root redirects to static/index.html"""
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307
    assert "/static/index.html" in response.headers["location"]


def test_get_activities(client):
    """Test fetching all activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]
    assert "max_participants" in data["Chess Club"]


def test_signup_success(client):
    """Test successful signup for an activity"""
    response = client.post(
        "/activities/Chess%20Club/signup",
        params={"email": "newstudent@mergington.edu"}
    )
    assert response.status_code == 200
    assert "Signed up newstudent@mergington.edu for Chess Club" in response.json()["message"]
    
    # Verify participant was added
    activities = client.get("/activities").json()
    assert "newstudent@mergington.edu" in activities["Chess Club"]["participants"]


def test_signup_duplicate(client):
    """Test that a student cannot sign up twice for the same activity"""
    email = "duplicate@mergington.edu"
    
    # First signup should succeed
    response1 = client.post(
        "/activities/Chess%20Club/signup",
        params={"email": email}
    )
    assert response1.status_code == 200
    
    # Second signup with same email should fail
    response2 = client.post(
        "/activities/Chess%20Club/signup",
        params={"email": email}
    )
    assert response2.status_code == 400
    assert "already signed up" in response2.json()["detail"]


def test_signup_nonexistent_activity(client):
    """Test signup for an activity that doesn't exist"""
    response = client.post(
        "/activities/Fake%20Activity/signup",
        params={"email": "test@mergington.edu"}
    )
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_unregister_success(client):
    """Test successful unregistration from an activity"""
    email = "unregister@mergington.edu"
    
    # First, sign up
    client.post(
        "/activities/Chess%20Club/signup",
        params={"email": email}
    )
    
    # Then unregister
    response = client.delete(
        "/activities/Chess%20Club/unregister",
        params={"email": email}
    )
    assert response.status_code == 200
    assert f"Removed {email} from Chess Club" in response.json()["message"]
    
    # Verify participant was removed
    activities = client.get("/activities").json()
    assert email not in activities["Chess Club"]["participants"]


def test_unregister_not_registered(client):
    """Test unregistering a student who isn't registered"""
    response = client.delete(
        "/activities/Chess%20Club/unregister",
        params={"email": "notregistered@mergington.edu"}
    )
    assert response.status_code == 404
    assert "not registered" in response.json()["detail"]


def test_unregister_nonexistent_activity(client):
    """Test unregistering from an activity that doesn't exist"""
    response = client.delete(
        "/activities/Fake%20Activity/unregister",
        params={"email": "test@mergington.edu"}
    )
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]
