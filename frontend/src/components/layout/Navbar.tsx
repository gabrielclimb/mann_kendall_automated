import { Home, FileSpreadsheet, Camera, Settings, TrendingUp } from 'lucide-react';

import { NavLink } from '../common/NavLink';

export const Navbar = () => {
    return (
        <nav className="bg-white shadow-sm">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex justify-between h-16">
                    <div className="flex">
                        {/* Logo */}
                        <div className="flex items-center">
                            <TrendingUp className="h-8 w-8 text-blue-600" />
                            <span className="ml-2 text-xl font-bold text-gray-900">MKA</span>
                        </div>

                        {/* Navigation Links */}
                        <div className="hidden sm:ml-6 sm:flex sm:space-x-8">
                            <NavLink to="/">
                                <Home className="h-5 w-5 mr-1" />
                                Home
                            </NavLink>
                            <NavLink to="/projects">
                                <FileSpreadsheet className="h-5 w-5 mr-1" />
                                Projects
                            </NavLink>
                            <NavLink to="/analysis">
                                <Camera className="h-5 w-5 mr-1" />
                                Analysis
                            </NavLink>
                        </div>
                    </div>

                    {/* Settings */}
                    <div className="flex items-center">
                        <button className="p-2 rounded-full text-gray-500 hover:text-gray-600">
                            <Settings className="h-6 w-6" />
                        </button>
                    </div>
                </div>
            </div>
        </nav>
    );
};
