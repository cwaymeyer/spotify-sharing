from flask import Blueprint, render_template, redirect
from flask_login import login_required
from models import db, User, Group, UserGroup
from forms import NewGroupForm

user_routes = Blueprint("user_routes", __name__, static_folder="../static", template_folder="../templates/user_page")


@user_routes.route("/user/<int:user_id>")
@login_required
def user_page(user_id):
    """Home page for logged in user."""

    user = User.query.get(user_id)

    return render_template("user-page.html", user=user)


@user_routes.route("/user/<int:user_id>/new-group", methods=["GET", "POST"])
@login_required
def create_new_group(user_id):
    """Create a new group."""

    user = User.query.get(user_id)
    form = NewGroupForm()

    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data

        newGroup = Group(name=name, description=description, admin_id=user_id)
        db.session.add(newGroup)
        db.session.commit()

        newUserGroup = UserGroup(user_id=user_id, group_id=newGroup.id)
        db.session.add(newUserGroup)
        db.session.commit()

        return redirect(f"/user/{user_id}")

    return render_template("create-group.html", user=user, form=form)


@user_routes.route("/user/<int:user_id>/browse-groups")
@login_required
def browse_created_groups(user_id):
    """Browse all created groups."""

    user = User.query.get(user_id)

    joinedGroups = UserGroup.query.filter_by(user_id=user_id).all()
    joinedGroupsIds = [group.group_id for group in joinedGroups]
    groups = Group.query.filter(Group.admin_id != user_id).filter(Group.id.notin_(joinedGroupsIds)).all()

    return render_template("browse-groups.html", user=user, groups=groups)