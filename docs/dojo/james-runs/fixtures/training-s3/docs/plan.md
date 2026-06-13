# Project Dashboard MVP Plan

## Goal

Build a small authenticated project dashboard that lets a logged-in user view,
create, update, and delete project records.

## Scope

The first version includes:

- A login screen.
- A dashboard page that lists the current user's projects.
- A project form for creating and editing records.
- Persistent storage for project records.
- Basic empty, loading, success, and error states.

## Terms

- **User:** A person with login credentials for this application.
- **Project record:** A saved item owned by one user with these fields:
  `id`, `owner_id`, `name`, `status`, `summary`, `created_at`, and
  `updated_at`.
- **Status:** One of `planned`, `active`, `paused`, or `done`.
- **Dashboard:** The authenticated page where the user sees and manages their
  project records.
- **Done:** The user can complete the acceptance checks below without manual
  database edits or developer intervention.

## Non-Goals

- Team sharing, permissions beyond record ownership, billing, analytics,
  notifications, and public project pages are not part of this MVP.
- Single sign-on, social login, password reset, email verification, and signup
  are not required. Email and password login is enough.
- Advanced visual design is not required. The UI only needs to be clear,
  responsive, and consistent with the rest of the application.

## Implementation Steps

1. Add authentication.
   - Provide email and password login.
   - Seed two verification users:
     `user-a@example.test` / `password-a` and
     `user-b@example.test` / `password-b`.
   - Redirect unauthenticated users away from the dashboard.
   - Show a clear error when login fails.
2. Add the project data model.
   - Store each project record with the fields listed in `Terms`.
   - Associate every record with exactly one `owner_id`.
   - Prevent users from reading or changing records owned by another user.
3. Build the dashboard page.
   - Show the current user's project records in a list or table.
   - Include each project's `name`, `status`, `summary`, and last updated time.
   - Show an empty state when the user has no projects.
4. Build create and edit flows.
   - Require `name` and `status`.
   - Accept only the status values listed in `Terms`.
   - Allow `summary` to be blank.
   - Show validation errors before saving invalid records.
   - Return the user to the dashboard after a successful save.
5. Build delete flow.
   - Ask for confirmation before deleting a project.
   - Remove the deleted record from the dashboard without requiring a full page
     refresh.
6. Verify the MVP.
   - Run the automated test suite if the fixture has one.
   - Manually complete the acceptance checks below.

## Acceptance Checks

- An unauthenticated visitor cannot open the dashboard.
- A user can log in with the seeded credentials for `user-a@example.test`.
- A failed login shows an error and does not open the dashboard.
- A logged-in user can create a project with `name`, `status`, and `summary`.
- The new project appears on the dashboard after saving.
- The project remains visible after logging out and logging back in.
- A user can edit a project's `name`, `status`, and `summary`.
- A user can delete a project after confirming the delete action.
- `user-a@example.test` cannot view, edit, or delete records owned by
  `user-b@example.test`.
- Empty, loading, validation-error, and save-error states are visible and
  understandable.
