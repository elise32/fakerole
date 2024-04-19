import re

from fakerole.fake_role_storage_helper import FakeRoleStorageHelper

class NameSizeError(Exception):
    pass

class MemberSizeError(Exception):
    pass

class IDSizeError(Exception):
    pass

def _is_valid_members_set(members: set[str]) -> bool:
    return (
        members
        and len(members) <= FakeRole.MEMBERS_MAX_SIZE
        and all(is_valid_member(member) for member in members)
    )
    
def is_valid_member(member:str) -> bool:
    """
    Checks if member is a valid Discord snowflake
    """
    return bool(re.match(r'^[0-9]{17,20}$', member))

class FakeRole:
    """
    These maxima are not chosen arbitrarily. Discord's maximum bot message size is 2000 characters.
    The markdown to hide pings takes 1000 characters. Ping markdown will be a max of 21 characters
    until 2090. 2000-1000-(21*40) = 160 characters, enough for 30 characters, 6 emoji, and change
    """
    NAME_MAX_LENGTH = 30
    MEMBERS_MAX_SIZE = 40

    def __init__(self, id: str, name: str, members: set[str], create_in_storage=True):
        if not id:
            raise IDSizeError("ID for FakeRole cannot be empty")
        self._id: str = id

        if not name or len(name) > self.NAME_MAX_LENGTH:
            raise NameSizeError(f"Name for FakeRole {self.id} {self.name} was incorrect, tried to \
                                set it to {name}, must be <= {self.NAME_MAX_LENGTH}")
        self._name: str = name

        if not _is_valid_members_set(members):
            raise MemberSizeError(f"Member size for FakeRole {self.id} {self.name} was incorrect, \
                                  was {len(members)}")
        self._members: set[str] = members

        if create_in_storage:
            storage_helper.create_group(self.id, self.name, self.members)
    
    @property
    def id(self):
        return self._id
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name:str):
        if not name or len(name) > self.NAME_MAX_LENGTH:
            raise NameSizeError(f"Name for FakeRole {self.id} {self.name} was incorrect, tried to \
                                set it to {name}, must be <= {self.NAME_MAX_LENGTH}")
        if name == self._name:
            return

        self._name = name
        storage_helper.change_group_name(self.id, name)

    @property
    def members(self) -> frozenset:
        return frozenset(self._members)
    
    def add(self, member) -> bool:
        """
        Adds member to fake role and updates the storage.
        Returns whether or not the member was successfully added.
        """
        # Sanity check
        if len(self.members) > FakeRole.MEMBERS_MAX_SIZE:
            raise MemberSizeError("Somehow, the FakeRole was above capacity")
        if len(self.members) == FakeRole.MEMBERS_MAX_SIZE:
            return False
        if not is_valid_member(member):
            return False
        
        self._members.add(member)
        storage_helper.add_member(self.id, member)
        return True
    
    def remove(self, member) -> bool:
        """
        Removes member to fake role and updates the storage. Deletes the group from storage if group
        become empty
        Returns whether the member was successfully removed. 
        """
        if not is_valid_member(member):
            return False
        
        self._members.remove(member)
        FakeRoleStorageHelper.remove_member(self.id, member)
        if not self.members:
            self.delete()
        return True
    
    def delete(self) -> bool:
        """
        Returns whether the FakeRole was successfully deleted
        """
        return storage_helper.delete_group(self.id)
    
    def __str__(self):
        return self.id + ',' + self.name + ',' + str(self._members)

def fetch_all_FakeRoles() -> list[FakeRole]:
    return [
            FakeRole(id, name, members, create_in_storage=False)
            for id, name, members
            in storage_helper.get_all()
    ]

storage_helper = FakeRoleStorageHelper()