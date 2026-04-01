# System Context
## Overview

This project is an academic management backend built using XanoScript and Spec-
Driven Development.

## Purpose
Allow users to manage academic subjects and related data with proper ownership and access controls.
## Core Entities
- Users (native Xano authentication with roles and account membership)
- Accounts (groups of users)
- Subjects (academic disciplines owned by users with configurable visibility)
- Event Logs (audit trail for user actions)
- Agent Conversations/Messages (AI interaction logs)
## Relationships
- Users belong to Accounts
- Subjects belong to Users and optionally linked to Accounts for sharing
- Subjects have visibility levels: private (owner only), account (account members), public (all users)
- All entities support audit logging via Event Logs
## Security Model
- Authentication via Xano auth tokens
- Ownership-based access control for subjects
- Role-based permissions within accounts
- Data isolation between users and accounts
## Expected Evolution
The system will later include advanced analytics, automation workflows, and third-party integrations for academic management.